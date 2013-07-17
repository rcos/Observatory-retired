Exec {
    path => "/usr/bin"
}

node "test.rcos.rpi.edu" {
    class {"apt":}
    class {"observatory":}
    class {"uwsgi":}
    class {"nginx":}

    Class["apt"] -> Class["observatory"]
    Class["observatory"] -> Class["uwsgi"]
    Class["apt"] -> Class["nginx"]
}

node default {

}
