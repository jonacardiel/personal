package com.dndforger.model

import java.io.Serializable

data class Currency(
    var platinum: Int = 0,
    var gold: Int = 0,
    var electrum: Int = 0,
    var silver: Int = 0,
    var copper: Int = 0
) : Serializable
