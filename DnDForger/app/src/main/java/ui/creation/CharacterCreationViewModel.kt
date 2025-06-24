package com.example.dndcharactermaker.ui.creation

import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.dndcharactermaker.data.local.entity.Character
import com.example.dndcharactermaker.data.repository.CharacterRepository
import kotlinx.coroutines.launch

class CharacterCreationViewModel(private val repository: CharacterRepository) : ViewModel() {

    // LiveData to hold the character being built
    val characterInProgress = MutableLiveData<Character>(Character())

    // LiveData for ability score generation
    val abilityScores = MutableLiveData<Map<String, Int>>()

    fun updateName(name: String) {
        characterInProgress.value?.name = name
    }

    fun selectRace(race: String, subRace: String) {
        val currentChar = characterInProgress.value ?: return
        currentChar.race = race
        currentChar.subRace = subRace
        // Here you would apply racial bonuses based on your JSON data
        // e.g., updateAbilityScore("CON", 2)
        characterInProgress.postValue(currentChar)
    }

    fun selectClass(className: String) {
        val currentChar = characterInProgress.value ?: return
        currentChar.className = className
        // Here you would set HP based on hit die, proficiencies, etc.
        characterInProgress.postValue(currentChar)
    }

    // Example for ability scores (Point Buy, Standard Array, Roll)
    fun setStandardArray() {
        abilityScores.value = mapOf("STR" to 15, "DEX" to 14, "CON" to 13, "INT" to 12, "WIS" to 10, "CHA" to 8)
    }

    fun saveCharacter() {
        viewModelScope.launch {
            characterInProgress.value?.let {
                // Apply final ability scores to character object
                it.strength = abilityScores.value?.get("STR") ?: 10
                // ... etc for other scores

                repository.insert(it)
            }
        }
    }
}

// You will need a ViewModelFactory to pass the repository to the ViewModel