variable "account_id" {
 type = string
 default = "xxxxxxxxxxxxx"
}

variable "region" {
 type = string
 default = "eu-central-1"
}

variable "networks" {
 description = "AWS subnets"
 type = map
 default     = {
                 first = {
                   "cidr_block" = "10.0.1.0/24",
                   "availability_zone" = "a"
                 },
                 second = {
                   "cidr_block" = "10.0.2.0/24",
                   "availability_zone" = "b"
                 },
                 third = {
                   "cidr_block" = "10.0.3.0/24",
                   "availability_zone" = "c"
                 }
               }
}

variable "db_username" {
 description = "The username for the DB master user"
 type        = string
 default = "xxxxxxxxx"
 sensitive = true
}
variable "db_password" {
 description = "The password for the DB master user"
 type        = string
 default = "xxxxxxxxxx"
 sensitive = true
}