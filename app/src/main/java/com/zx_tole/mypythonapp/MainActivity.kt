package com.zx_tole.mypythonapp

import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import com.zx_tole.mypythonapp.repository.HabitRepository
import com.zx_tole.mypythonapp.ui.HabitTrackerScreen
import com.zx_tole.mypythonapp.ui.theme.MyPythonAppTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MyPythonAppTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    val repository = remember { HabitRepository() }
                    HabitTrackerScreen(
                        modifier = Modifier.padding(innerPadding),
                        repository = repository,
                        onShowToast = { message ->
                            Toast.makeText(this@MainActivity, message, Toast.LENGTH_SHORT).show()
                        }
                    )
                }
            }
        }
    }
}
