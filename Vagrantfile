VAGRANTFILE_API_VERSION = "2"

base_dir = File.expand_path(File.dirname(__FILE__))
cluster = {
  "ubuntu-hl7v2" => { :cpus => 1, :mem => 1024 }

}

hostMachine = "#{`hostname`[0..-2]}".sub(/\..*$/,'') + "-"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  if Vagrant.has_plugin?("vagrant-cachier")
    config.cache.scope = :machine
    config.cache.enable :apt
  end


  cluster.each do |hostname, info|

    config.vm.define  hostMachine + hostname  do |cfg|

      cfg.vm.provider :virtualbox do |vb, override|
        override.vm.box = "ubuntu/wily64"
        override.vm.hostname = hostMachine + hostname

        override.vm.network "public_network", bridge: [
        "en0: Wi-Fi (AirPort)",
        "en6: Broadcom NetXtreme Gigabit Ethernet Controller",
        ]

        vb.name =  hostMachine + hostname
        vb.customize ["modifyvm", :id, "--memory", info[:mem], "--cpus", info[:cpus], "--hwvirtex", "on" ]
      end

      #PDF-Miner
      config.vm.provision "pdf-miner", type: "ansible" do |ansible|
        ansible.playbook = "ansible/install-pdfMiner.yml"
        ansible.sudo = true
      end

    end

  end

end
