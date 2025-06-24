package com.example.dndcharactherforger // This is your correct package name

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.Spinner
import android.widget.TextView
import kotlin.math.floor
import com.example.dndcharactherforger.R // <-- THIS IS THE CORRECTED LINE

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // This line connects our Kotlin code to our XML layout file.
        setContentView(R.layout.activity_main)

        // --- 1. Find our UI elements from the XML layout ---
        // We use findViewById to get a reference to each View so we can control it.
        val nameEditText = findViewById<EditText>(R.id.nameEditText)
        val raceSpinner = findViewById<Spinner>(R.id.raceSpinner)
        val strengthEditText = findViewById<EditText>(R.id.strengthEditText)
        val calculateButton = findViewById<Button>(R.id.calculateButton)
        val resultTextView = findViewById<TextView>(R.id.resultTextView)

        // --- 2. Set up the data for our Race dropdown (Spinner) ---
        // In a real app, this would come from a database or JSON file.
        // For now, we just create a simple list of strings.
        val races = listOf("Human", "Elf", "Dwarf", "Halfling", "Dragonborn", "Gnome", "Tiefling")

        // An "Adapter" is needed to adapt our list of strings into something the Spinner can display.
        val raceAdapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, races)
        raceAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)

        // Connect the adapter to our spinner.
        raceSpinner.adapter = raceAdapter

        // --- 3. Set up the button's click listener ---
        // This block of code will run every time the user clicks the button.
        calculateButton.setOnClickListener {
            // Get the current text from the input fields
            val characterName = nameEditText.text.toString()
            val selectedRace = raceSpinner.selectedItem.toString()

            // Get the strength score. toIntOrNull() is safe: if the box is empty, it becomes null.
            // The `?: 10` part means "if it's null, use 10 as a default value".
            val strengthScore = strengthEditText.text.toString().toIntOrNull() ?: 10

            // Calculate the ability modifier. The D&D 5e formula is (score - 10) / 2, rounded down.
            val strengthModifier = floor((strengthScore - 10) / 2.0).toInt()

            // Create the modifier string, adding a "+" sign if it's positive.
            val modifierText = if (strengthModifier >= 0) "+$strengthModifier" else "$strengthModifier"

            // Build the final result string to display.
            val resultString = """
                Character: $characterName, $selectedRace
                Strength: $strengthScore ($modifierText)
            """.trimIndent() // trimIndent() cleans up the whitespace from the multiline string.

            // Set the text of our result TextView to show the final string.
            resultTextView.text = resultString
        }
    }
}