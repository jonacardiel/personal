package com.dndforger.db

import androidx.room.TypeConverter
import com.dndforger.model.AbilityScores
import com.dndforger.model.Currency
import com.dndforger.model.EquipmentItem
import com.dndforger.model.SpellSlot
import com.google.firebase.crashlytics.buildtools.reloc.com.google.common.reflect.TypeToken
import com.google.gson.Gson
import java.lang.reflect.Type

class Converters {
    private val gson = Gson()

    // List<String>
    @TypeConverter
    fun fromStringList(value: List<String>?): String? = gson.toJson(value)
    @TypeConverter
    fun toStringList(value: String?): List<String>? =
        gson.fromJson(value, object : TypeToken<List<String>>() {}.type)

    // Map<String, Int>
    @TypeConverter
    fun fromStringIntMap(value: Map<String, Int>?): String? = gson.toJson(value)
    @TypeConverter
    fun toStringIntMap(value: String?): List<String>? =
        gson.fromJson(value, object : TypeToken<Map<String, Int>>() {}.type)

    // Map<String, Boolean>
    @TypeConverter
    fun fromStringBooleanMap(value: Map<String, Boolean>?): String? = gson.toJson(value)
    @TypeConverter
    fun toStringBooleanMap(value: String?): List<String>? =
        gson.fromJson(value, object : TypeToken<Map<String, Boolean>>() {}.type)

    // List<EquipmentItem>
    @TypeConverter
    fun fromEquipmentItemList(value: List<EquipmentItem>?): String? = gson.toJson(value)
    @TypeConverter
    fun toEquipmentItemList(value: String?): List<String>? =
        gson.fromJson(value, object : TypeToken<List<EquipmentItem>>() {}.type)

    // List<SpellSlot>
    @TypeConverter
    fun fromSpellSlotList(value: List<SpellSlot>?): String? = gson.toJson(value)
    @TypeConverter
    fun toSpellSlotList(value: String?): List<String>? =
        gson.fromJson(value, object : TypeToken<List<SpellSlot>>() {}.type)

    // AbilityScores
    @TypeConverter
    fun fromAbilityScores(value: AbilityScores?): String? = gson.toJson(value)
    @TypeConverter
    fun toAbilityScores(value: String?): List<String>? =
        gson.fromJson(value, AbilityScores::class.java)

    // Currency
    @TypeConverter
    fun fromCurrency(value: Currency?): String? = gson.toJson(value)
    @TypeConverter
    fun toCurrency(value: String?): Currency? =
        gson.fromJson(value, Currency::class.java)
}