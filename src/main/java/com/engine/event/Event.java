package com.engine.event;

public abstract class Event {
    private static long eCount=0;
    private static long genID(){
        return eCount++;
    }

    public int type;

    public Event(int type){
        this.type = type;
    }

    public abstract void handleEvent() throws InterruptedException;

}
