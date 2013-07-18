Exec {
    path => "/usr/bin"
}

node "test.rcos.rpi.edu" {
    class {"apt":}
    class {"nginx":}
    class {"uwsgi":}
    class {"observatory::dir":}
    class {"observatory":}

    Class["apt"] -> Class["nginx"]
    Class["apt"] -> Class["observatory"]
    Class["observatory"] -> Class["uwsgi"]
}

node default {

}
