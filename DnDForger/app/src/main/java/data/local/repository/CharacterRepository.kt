package com.example.dndcharactermaker.data.repository

import androidx.lifecycle.LiveData
import com.example.dndcharactermaker.data.local.dao.CharacterDao
import com.example.dndcharactermaker.data.local.entity.Character

// The repository is the single source of truth.
// For now it only gets data from the local DB.
// Later, it could fetch from a remote API.
class CharacterRepository(private val characterDao: CharacterDao) {

    val allCharacters: LiveData<List<Character>> = characterDao.getAllCharacters()

    fun getCharacterById(id: Long): LiveData<Character> {
        return characterDao.getCharacterById(id)
    }

    suspend fun insert(character: Character) {
        characterDao.insertCharacter(character)
    }

    suspend fun update(character: Character) {
        characterDao.updateCharacter(character)
    }

    suspend fun delete(character: Character) {
        characterDao.deleteCharacter(character)
    }
}