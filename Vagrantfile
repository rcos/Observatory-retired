# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "precise32"
  #config.vm.hostname = "rcos.rpi.edu"
  config.vm.hostname = "test.rcos.rpi.edu"
  config.vm.box_url = "http://files.vagrantup.com/precise32.box"

  config.vm.network :private_network, ip: "192.168.56.2"
  config.vm.network :forwarded_port, guest: 80, host: 8000


  config.vm.provider :virtualbox do |vb|
      vb.customize [
        "modifyvm", :id,
        "--memory", "1024",
        "--cpus", "1"]
  end

  config.vm.provision :puppet do |puppet|
     puppet.manifests_path = "puppet"
     puppet.manifest_file  = "base.pp"
     puppet.module_path    = "modules"
     puppet.options        = ""
  end
end
