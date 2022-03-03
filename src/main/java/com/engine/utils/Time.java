package com.engine.utils;

public class Time {

    public static float timeStarted = System.nanoTime();
    public static float deltaTime;

    public static float getTime(){
        return (float)((System.nanoTime() - timeStarted) * 1E-9);
    }

    private static float endTime, startTime;

    public static void start(){
        startTime = getTime();
    }

    public static void update(){
        endTime = getTime();
        deltaTime = endTime - startTime;
    }

}
