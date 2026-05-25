//
// Created by Shrekulka on 13.12.2023.
//

#pragma once

#ifndef REVERSE_SOCKS5_PROXY_STDAFX_H
#define REVERSE_SOCKS5_PROXY_STDAFX_H

#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <sys/ioctl.h>
#include <sys/eventfd.h>

#include <task.h>
#include <task-io.h>
#include <task-io-socket.h>
#include <task-dns.h>
#include <task-system.h>
#include <memory-allocator.h>

#include "list.h"
#include "rbtree.h"
#include "config.h"
#include "logger.h"
#include "compiler.h"
#include "config-const.h"
#include "tsocks-cache.h"
#include "socks5-session-tcp.h"
#include "socks5-session-udp.h"
#include "tproxy-session-dns.h"
#include "reverse_socks5_tproxy.h"


#include <yaml.h>


#endif //REVERSE_SOCKS5_PROXY_STDAFX_H
