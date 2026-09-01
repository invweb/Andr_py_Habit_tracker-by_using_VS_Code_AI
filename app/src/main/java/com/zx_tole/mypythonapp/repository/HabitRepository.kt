package com.zx_tole.mypythonapp.repository

import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import java.text.SimpleDateFormat
import java.util.Locale
import java.util.*

data class Habit(
    val id: String,
    val name: String,
    val completedDates: List<String>,
    val createdAt: String
) {
    val isCompletedToday: Boolean
        get() {
            val today = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(Date())
            return completedDates.contains(today)
        }
    
    val streak: Int
        get() {
            if (completedDates.isEmpty()) return 0
            
            val sortedDates = completedDates.sortedDescending()
            val calendar = Calendar.getInstance().apply { time = Date() }
            calendar.set(Calendar.HOUR_OF_DAY, 0)
            calendar.set(Calendar.MINUTE, 0)
            calendar.set(Calendar.SECOND, 0)
            calendar.set(Calendar.MILLISECOND, 0)
            val today = calendar.time
            val yesterday = Calendar.getInstance().apply {
                time = today
                add(Calendar.DAY_OF_YEAR, -1)
            }.time
            
            val localFormat = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
            val lastCompleted = localFormat.parse(sortedDates[0])!!
            if (lastCompleted.time != today.time && lastCompleted.time != yesterday.time) return 0
            
            var count = 1
            var currentDate = lastCompleted
            for (i in 1 until sortedDates.size) {
                val prevDate = localFormat.parse(sortedDates[i])!!
                val expectedDate = Calendar.getInstance().apply {
                    time = currentDate
                    add(Calendar.DAY_OF_YEAR, -1)
                }.time
                
                if (prevDate.time == expectedDate.time) {
                    count++
                    currentDate = prevDate
                } else {
                    break
                }
            }
            return count
        }
    
    val totalCompleted: Int
        get() = completedDates.size
}

class HabitRepository {
    private val _habits = MutableStateFlow<Map<String, Habit>>(emptyMap())
    val habits: StateFlow<Map<String, Habit>> = _habits.asStateFlow()
    
    private val dateFormat = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
    private val idFormat = SimpleDateFormat("yyyyMMddHHmmss", Locale.getDefault())
    
    fun addHabit(name: String) {
        val id = idFormat.format(Date())
        val habit = Habit(
            id = id,
            name = name,
            completedDates = emptyList(),
            createdAt = dateFormat.format(Date())
        )
        val updated = _habits.value.toMutableMap()
        updated[id] = habit
        _habits.value = updated
    }
    
    fun removeHabit(habitId: String) {
        val updated = _habits.value.toMutableMap()
        updated.remove(habitId)
        _habits.value = updated
    }
    
    fun toggleHabit(habitId: String) {
        val habit = _habits.value[habitId] ?: return
        val today = dateFormat.format(Date())
        val updatedDates = if (habit.completedDates.contains(today)) {
            habit.completedDates - today
        } else {
            habit.completedDates + today
        }
        
        val updatedHabit = habit.copy(completedDates = updatedDates)
        val updated = _habits.value.toMutableMap()
        updated[habitId] = updatedHabit
        _habits.value = updated
    }
    
    fun getAllHabits(): Map<String, Habit> {
        return _habits.value
    }
}
