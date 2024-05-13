terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  project = "neat-vista-422604-c3"
}

# Create vpc1
resource "google_compute_network" "vpc1" {
  name                    = "vpc1"
  auto_create_subnetworks = false
}

# Create vpc2
resource "google_compute_network" "vpc2" {
  name                    = "vpc2"
  auto_create_subnetworks = false
}

# Create subnet1
resource "google_compute_subnetwork" "subnet1" {
  name          = "subnet1"
  ip_cidr_range = "10.1.0.0/24"
  network       = google_compute_network.vpc1.self_link
  region        = "us-west1"
}

# Create subnet2
resource "google_compute_subnetwork" "subnet2" {
  name          = "subnet2"
  ip_cidr_range = "10.2.0.0/24"
  network       = google_compute_network.vpc2.self_link
  region        = "us-west1"
}

# Resource definition for a Google Compute Engine instance in vpc1
resource "google_compute_instance" "vm1" {
  name         = "vm1"
  machine_type = "e2-micro"
  zone         = "us-west1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-10" # Specify the boot disk image
    }
  }

  # Specify the network interface for vm1
  network_interface {
    network    = google_compute_network.vpc1.self_link
    subnetwork = google_compute_subnetwork.subnet1.self_link
    access_config {
      // Ephemeral IP
    }
  }

  # Upload the private key file to the instance
  /*provisioner "file" {
    source      = "./terraform_key"
    destination = "/tmp/terraform_key" # Destination path on the instance

    # Specify connection configuration
    connection {
      type        = "ssh"
      user        = "ssh_user"
      private_key = file("./terraform_key")
      host        = self.network_interface[0].access_config[0].nat_ip
    }

  }

  # Enable SSH By Setting the SSH Public Key File Path
  metadata = {
    ssh-keys = "ssh_user:./terraform_key.pub"
  }*/

  metadata_startup_script = "sudo apt-get update; sudo apt-get install auditd -y; sudo systemctl start auditd; sudo systemctl enable auditd"

  /*provisioner "remote-exec" {
    inline = ["sudo apt update", "sudo apt install audit"]

    connection {
      type     = "ssh"
      port = 22
      user     = "ssh_user"
      password = ""
      host = self.network_interface[0].access_config[0].nat_ip
      private_key = "/tmp/terraform_key"
      timeout = "5m"
    }
  }
  provisioner "local-exec" {
	command = "ansible-playbook -i 35.230.91.235, playbook.yaml"
  }*/

}

# Resource definition for a Google Compute Engine instance in vpc1
resource "google_compute_instance" "vm2" {
  name         = "vm2"
  machine_type = "e2-micro"
  zone         = "us-west1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-10" # Specify the boot disk image
    }
  }

  # Specify the network interface for vm2
  network_interface {
    network    = google_compute_network.vpc2.self_link
    subnetwork = google_compute_subnetwork.subnet2.self_link
    access_config {
      // Ephemeral IP
    }
  }

  metadata_startup_script = "sudo apt-get update; sudo apt-get install auditd -y; sudo systemctl start auditd; sudo systemctl enable auditd"
}

# Routing node to connect vpcs
resource "google_compute_instance" "routing_node" {
  name         = "routing-node"
  machine_type = "e2-micro"
  zone         = "us-west1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-10" # Specify the boot disk image
    }
  }

  # Specify the network interface for routing node
  network_interface {
    network    = google_compute_network.vpc1.self_link
    subnetwork = google_compute_subnetwork.subnet1.self_link
    access_config {
      // Ephemeral IP
    }
  }

  # Specify the network interface for routing node
  network_interface {
    network    = google_compute_network.vpc2.self_link
    subnetwork = google_compute_subnetwork.subnet2.self_link
    access_config {
      // Ephemeral IP
    }
  }
}
