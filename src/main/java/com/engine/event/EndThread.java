package com.engine.event;

public class EndThread extends Event{


    public EndThread() {
        super(0);
    }

    @Override
    public void handleEvent() {
        System.out.println("Ending Process!");
    }
}
