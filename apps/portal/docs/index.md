---
title: 路书
layout: page
sidebar: false
aside: false
---

<script setup>
import { PortalHome } from '@lubook/theme'
import { PORTAL_CARDS, TAGLINE, INTRO } from '../content.config'
</script>

<PortalHome :cards="PORTAL_CARDS" :tagline="TAGLINE" :intro="INTRO" />
