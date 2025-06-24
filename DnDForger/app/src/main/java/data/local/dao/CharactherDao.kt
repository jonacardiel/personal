package com.example.dndcharactermaker.data.local.dao

import androidx.lifecycle.LiveData
import androidx.room.*
import com.example.dndcharactermaker.data.local.entity.Character

@Dao
interface CharacterDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertCharacter(character: Character): Long // Returns the new ID

    @Update
    suspend fun updateCharacter(character: Character)

    @Delete
    suspend fun deleteCharacter(character: Character)

    @Query("SELECT * FROM characters WHERE id = :characterId")
    fun getCharacterById(characterId: Long): LiveData<Character>

    @Query("SELECT * FROM characters ORDER BY name ASC")
    fun getAllCharacters(): LiveData<List<Character>>
}