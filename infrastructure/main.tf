provider "google" {
  credentials = file("./neat-vista-422604-c3-e68cc6362761.json")
  #credentials = file("./neat-vista-422604-c3-9d96dd40509a.json")
  project     = "neat-vista-422604-c3"
  region      = "us-west1"
}

# VPC 1
resource "google_compute_network" "vpc_network_1" {
  name                    = "terraform-network-1"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet_1a" {
  name          = "subnet-1a"
  ip_cidr_range = "10.0.1.0/24"
  region        = "us-west1"
  network       = google_compute_network.vpc_network_1.name
}

# VPC 2
resource "google_compute_network" "vpc_network_2" {
  name                    = "terraform-network-2"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet_2a" {
  name          = "subnet-2a"
  ip_cidr_range = "10.0.2.0/24"
  region        = "us-west1"
  network       = google_compute_network.vpc_network_2.name
}

resource "google_compute_network_peering" "peering1to2" {
  name         = "peering1to2"
  network      = google_compute_network.vpc_network_1.id
  peer_network = google_compute_network.vpc_network_2.self_link
  provisioner "local-exec" {
    command    = "sleep 30"
    on_failure = continue
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "google_compute_network_peering" "peering2to1" {
  name         = "peering2to1"
  network      = google_compute_network.vpc_network_2.id
  peer_network = google_compute_network.vpc_network_1.self_link
  provisioner "local-exec" {
    command    = "sleep 30"
    on_failure = continue
  }

  lifecycle {
    create_before_destroy = true
  }
}

# VM in Subnet 1a
resource "google_compute_instance" "vm_1a" {
  name         = "vm-1a"
  machine_type = "f1-micro"
  zone         = "us-west1-a"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2004-lts"
    }
  }

  network_interface {
    network    = google_compute_network.vpc_network_1.name
    subnetwork = google_compute_subnetwork.subnet_1a.name

    access_config {
      // Include this section to give the VM an external IP address
    }
  }

  metadata = {
    ssh-keys = "student:${file("~/.ssh/id_rsa_student.pub")}"
  }

  tags = ["student"]

  provisioner "remote-exec" {
    connection {
      type        = "ssh"
      user        = "student"
      private_key = file("~/.ssh/id_rsa_student")
      host        = google_compute_instance.vm_1a.network_interface[0].access_config[0].nat_ip
    }

    inline = [
      "sudo useradd -m student",
      "sudo mkdir /home/student/.ssh",
      "sudo cp /home/student/.ssh/authorized_keys /home/student/.ssh/",
      "sudo chown -R student:student /home/student/.ssh",
      "sudo chmod 700 /home/student/.ssh",
      "sudo chmod 600 /home/student/.ssh/authorized_keys"
    ]
  }
}

# VM in Subnet 2a
resource "google_compute_instance" "vm_2a" {
  name         = "vm-2a"
  machine_type = "f1-micro"
  zone         = "us-west1-a"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2004-lts"
    }
  }

  network_interface {
    network    = google_compute_network.vpc_network_2.name
    subnetwork = google_compute_subnetwork.subnet_2a.name

    access_config {
      // Include this section to give the VM an external IP address
    }
  }

  metadata = {
    ssh-keys = "professor:${file("~/.ssh/id_rsa_professor.pub")}"
  }

  tags = ["professor"]

  provisioner "remote-exec" {
    connection {
      type        = "ssh"
      user        = "professor"
      private_key = file("~/.ssh/id_rsa_professor")
      host        = google_compute_instance.vm_2a.network_interface[0].access_config[0].nat_ip
    }

    inline = [
      "sudo useradd -m professor",
      "sudo mkdir /home/professor/.ssh",
      "sudo cp /home/professor/.ssh/authorized_keys /home/professor/.ssh/",
      "sudo chown -R professor:professor /home/professor/.ssh",
      "sudo chmod 700 /home/professor/.ssh",
      "sudo chmod 600 /home/professor/.ssh/authorized_keys"
    ]
  }
}

# Firewall rules to allow SSH and port 8888 between VPCs

# SSH Firewall rule for VPC 1
resource "google_compute_firewall" "ssh_firewall_1" {
  name    = "ssh-firewall-1"
  network = google_compute_network.vpc_network_1.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["student"]
}

# Port 8888 Firewall rule for VPC 1
resource "google_compute_firewall" "allow-application" {
  name    = "allow-application"
  network = google_compute_network.vpc_network_1.name

  allow {
    protocol = "icmp"
  }

  source_ranges = ["0.0.0.0/0"]  // Adjust based on your network's CIDR or specific needs
  target_tags   = ["student"]
}

# SSH Firewall rule for VPC 2
resource "google_compute_firewall" "ssh_firewall_2" {
  name    = "ssh-firewall-2"
  network = google_compute_network.vpc_network_2.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["professor"]
}

# First null_resource for the first virtual machine
resource "null_resource" "ansible_playbook_vm_1a" {
  # Define the provisioner for the first VM
  provisioner "local-exec" {
    command = <<EOF
      export ANSIBLE_HOST_KEY_CHECKING=False
      ansible-playbook -vvv -i 'student@${google_compute_instance.vm_1a.network_interface[0].access_config[0].nat_ip},' --private-key ~/.ssh/id_rsa_student playbook.yml | tee ansible-log-vm1a.txt
    EOF
  }

  # Dependency to ensure the VM is ready before provisioning
  depends_on = [
    google_compute_instance.vm_1a
  ]
}

resource "null_resource" "ansible_playbook_vm_2a" {
  # Define the provisioner for the second VM
  provisioner "local-exec" {
    command = <<EOF
      export ANSIBLE_HOST_KEY_CHECKING=False
      ansible-playbook -vvv -i 'professor@${google_compute_instance.vm_2a.network_interface[0].access_config[0].nat_ip},' --private-key ~/.ssh/id_rsa_professor playbook.yml | tee ansible-log-vm2a.txt
    EOF
  }

  # Dependency to ensure the VM is ready before provisioning
  depends_on = [
    google_compute_instance.vm_2a
  ]
}



