class CharacterSheetViewModel(private val repository: CharacterRepository, characterId: Long) : ViewModel() {
    val character: LiveData<Character> = repository.getCharacterById(characterId)

    // Example calculation
    val strengthModifier: LiveData<Int> = Transformations.map(character) {
        floor((it.strength - 10) / 2.0).toInt()
    }
}