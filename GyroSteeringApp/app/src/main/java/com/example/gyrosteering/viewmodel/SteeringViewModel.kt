package com.example.gyrosteering.viewmodel

import androidx.lifecycle.ViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

class SteeringViewModel : ViewModel() {
    private val _steeringAngle = MutableStateFlow(0f)
    val steeringAngle: StateFlow<Float> = _steeringAngle.asStateFlow()

    private val _brakePressure = MutableStateFlow(0f)
    val brakePressure: StateFlow<Float> = _brakePressure.asStateFlow()

    private val _throttlePressure = MutableStateFlow(0f)
    val throttlePressure: StateFlow<Float> = _throttlePressure.asStateFlow()

    private val _centerOffset = MutableStateFlow(0f)

    fun updateRawSteering(angle: Float) {
        // Apply center offset
        var centeredAngle = angle - _centerOffset.value
        // Clamp between -90 and 90
        if (centeredAngle > 90f) centeredAngle = 90f
        if (centeredAngle < -90f) centeredAngle = -90f
        _steeringAngle.value = centeredAngle
    }

    fun setAsCenter(currentRawAngle: Float) {
        _centerOffset.value = currentRawAngle
    }

    fun updateBrake(pressure: Float) {
        _brakePressure.value = pressure.coerceIn(0f, 100f)
    }

    fun updateThrottle(pressure: Float) {
        _throttlePressure.value = pressure.coerceIn(0f, 100f)
    }
}
