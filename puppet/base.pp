Exec {
    path => "/usr/bin"
}

node "test.rcos.rpi.edu" {
    class {"apt":}
    class {"uwsgi":}
    class {"nginx":}

    Class["apt"] -> Class["uwsgi"]
    Class["apt"] -> Class["nginx"]
}

node default {

}
