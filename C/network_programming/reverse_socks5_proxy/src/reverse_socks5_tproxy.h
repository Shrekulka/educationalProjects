//
// Created by Shrekulka on 21.12.2023.
//
#pragma once

#include "stdafx.h"

#ifndef REVERSE_SOCKS5_PROXY_REVERSE_SOCKS5_TPROXY_H
#define REVERSE_SOCKS5_PROXY_REVERSE_SOCKS5_TPROXY_H

#define HEV_LIST_INIT { NULL, NULL }
#define HEV_RBTREE_INIT { NULL, NULL }

int hev_socks5_tproxy_init (void);
void hev_socks5_tproxy_fini (void);

void hev_socks5_tproxy_run (void);
void hev_socks5_tproxy_stop (void);

#endif //REVERSE_SOCKS5_PROXY_REVERSE_SOCKS5_TPROXY_H
