package com.example.gyrosteering

import android.content.Context
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import androidx.lifecycle.DefaultLifecycleObserver
import androidx.lifecycle.LifecycleOwner

class GyroSensorManager(
    private val context: Context,
    private val onAngleChanged: (Float) -> Unit
) : DefaultLifecycleObserver, SensorEventListener {

    private var sensorManager: SensorManager? = null
    private var rotationSensor: Sensor? = null

    init {
        sensorManager = context.getSystemService(Context.SENSOR_SERVICE) as SensorManager
        rotationSensor = sensorManager?.getDefaultSensor(Sensor.TYPE_ROTATION_VECTOR)
    }

    override fun onResume(owner: LifecycleOwner) {
        super.onResume(owner)
        rotationSensor?.let {
            sensorManager?.registerListener(this, it, SensorManager.SENSOR_DELAY_GAME)
        }
    }

    override fun onPause(owner: LifecycleOwner) {
        super.onPause(owner)
        sensorManager?.unregisterListener(this)
    }

    override fun onSensorChanged(event: SensorEvent?) {
        if (event?.sensor?.type == Sensor.TYPE_ROTATION_VECTOR) {
            val rotationMatrix = FloatArray(9)
            SensorManager.getRotationMatrixFromVector(rotationMatrix, event.values)
            val orientationAngles = FloatArray(3)
            SensorManager.getOrientation(rotationMatrix, orientationAngles)
            
            // Convert pitch to degrees for steering (phone held landscape)
            val pitchDegrees = Math.toDegrees(orientationAngles[1].toDouble()).toFloat()
            onAngleChanged(pitchDegrees)
        }
    }

    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {
        // Not needed
    }
}
