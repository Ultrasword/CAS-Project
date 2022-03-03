package com.engine.event;

public class NoEvents extends Event{
    private final static int eventID = 2;

    public NoEvents() {
        super(eventID);
    }

    @Override
    public void handleEvent() {
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
