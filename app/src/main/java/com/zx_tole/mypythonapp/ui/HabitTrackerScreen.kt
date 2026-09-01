package com.zx_tole.mypythonapp.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.zx_tole.mypythonapp.repository.Habit
import com.zx_tole.mypythonapp.repository.HabitRepository
import java.text.SimpleDateFormat
import java.util.*

@Composable
fun HabitTrackerScreen(
    modifier: Modifier = Modifier,
    repository: HabitRepository,
    onShowToast: (String) -> Unit
) {
    var habitName by remember { mutableStateOf("") }
    val habits by repository.habits.collectAsState()
    
    Column(
        modifier = modifier
            .fillMaxSize()
            .background(Color(0xFFF5F5F5))
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        // Заголовок
        Text(
            text = "🎯 Habit Tracker",
            fontSize = 28.sp,
            fontWeight = FontWeight.Bold,
            color = Color(0xFF2196F3),
            modifier = Modifier.padding(top = 24.dp, bottom = 8.dp)
        )
        
        // Дата
        val dateFormat = SimpleDateFormat("dd.MM.yyyy", Locale.getDefault())
        Text(
            text = dateFormat.format(Date()),
            fontSize = 14.sp,
            color = Color.Gray,
            modifier = Modifier.padding(bottom = 24.dp)
        )
        
        // Поле ввода
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            OutlinedTextField(
                value = habitName,
                onValueChange = { habitName = it },
                placeholder = { Text("Название привычки...") },
                modifier = Modifier.weight(1f),
                singleLine = true
            )
            
            Button(
                onClick = {
                    if (habitName.isNotBlank()) {
                        repository.addHabit(habitName)
                        habitName = ""
                        onShowToast("✅ Привычка добавлена!")
                    }
                },
                modifier = Modifier.align(Alignment.CenterVertically)
            ) {
                Icon(Icons.Default.Add, contentDescription = null)
                Spacer(modifier = Modifier.width(4.dp))
                Text("Добавить")
            }
        }
        
        // Список привычек
        LazyColumn(
            modifier = Modifier.weight(1f),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(habits.keys.toList(), key = { it }) { habitId ->
                val habit = habits[habitId]
                if (habit != null) {
                    HabitItem(
                        habit = habit,
                        onToggle = { repository.toggleHabit(habitId) },
                        onDelete = {
                            repository.removeHabit(habitId)
                            onShowToast("🗑 Привычка удалена")
                        }
                    )
                }
            }
        }
        
        // Статистика
        val completedCount = habits.values.count { it.isCompletedToday }
        Text(
            text = "Сегодня: $completedCount/${habits.size} выполнено",
            fontSize = 14.sp,
            color = Color.Gray,
            modifier = Modifier.padding(top = 16.dp)
        )
    }
}

@Composable
fun HabitItem(
    habit: Habit,
    onToggle: () -> Unit,
    onDelete: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp),
        colors = CardDefaults.cardColors(
            containerColor = if (habit.isCompletedToday) Color(0xFFE8F5E9) else Color.White
        )
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Статус
            Text(
                text = if (habit.isCompletedToday) "✅" else "⬜",
                fontSize = 20.sp,
                modifier = Modifier.padding(end = 12.dp)
            )
            
            // Название
            Text(
                text = habit.name,
                fontSize = 16.sp,
                fontWeight = FontWeight.Medium,
                color = if (habit.isCompletedToday) Color.Gray else Color.Black,
                modifier = Modifier.weight(1f)
            )
            
            // Стрик
            if (habit.streak > 0) {
                Text(
                    text = "🔥 ${habit.streak}",
                    fontSize = 14.sp,
                    color = Color(0xFFFF9800),
                    modifier = Modifier.padding(end = 8.dp)
                )
            }
            
            // Всего
            Text(
                text = "${habit.totalCompleted}",
                fontSize = 12.sp,
                color = Color.Gray,
                modifier = Modifier.padding(end = 8.dp)
            )
            
            // Кнопки
            IconButton(onClick = onToggle) {
                Icon(
                    Icons.Default.Check,
                    contentDescription = "Toggle",
                    tint = if (habit.isCompletedToday) Color.Green else Color.Gray
                )
            }
            
            IconButton(onClick = onDelete) {
                Icon(
                    Icons.Default.Delete,
                    contentDescription = "Delete",
                    tint = Color.Red
                )
            }
        }
    }
}
