Exec {
    path => "/usr/bin"
}

class {"apt":}
class {"nginx":}
class {"uwsgi":}

Class["apt"] -> Class["nginx"]

node "test.rcos.rpi.edu" {
    class {"observatory::dir":}
    class {"observatory":}
    Class["observatory"] -> Class["uwsgi"]
    Class["apt"] -> Class["observatory"]

}

node "rcos.rpi.edu" {

    class {"ssh":}

    class {"deploy":
        repo    => "git://github.com/rcos/Observatory.git",
    }

    class {"observatory::dir":
        source => "/home/deploy/Observatory/observatory"
    }

    Class["deploy"] -> Class["observatory::dir"]
    class {"observatory":}
    Class["observatory"] -> Class["uwsgi"]
    Class["apt"] -> Class["observatory"]
}


