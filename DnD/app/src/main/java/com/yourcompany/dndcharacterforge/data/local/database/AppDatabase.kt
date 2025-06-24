package com.yourcompany.dndcharacterforge.data.local.database

import androidx.room.Database
import androidx.room.RoomDatabase
import com.yourcompany.dndcharacterforge.data.local.dao.CharacterDao
import com.yourcompany.dndcharacterforge.data.local.entities.CharacterEntity

@Database(entities = [CharacterEntity::class], version = 1, exportSchema = false)
abstract class AppDatabase : RoomDatabase() {
    abstract fun characterDao(): CharacterDao
}
