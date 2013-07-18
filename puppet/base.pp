Exec {
    path => "/usr/bin"
}

node "test.rcos.rpi.edu" {
    class {"apt":}
    class {"observatory":}
    class {"uwsgi":}
    class {"nginx":}

    Class["apt"] -> Class["nginx"]
    Class["nginx"] -> Class["observatory"]
    Class["observatory"] -> Class["uwsgi"]
}

node default {

}
