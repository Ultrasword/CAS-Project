package com.engine.event;

import java.util.concurrent.ConcurrentLinkedQueue;

public class EventQueue {

    private final static ConcurrentLinkedQueue<Event> eventQueue = new ConcurrentLinkedQueue<>();

    public static Event getEvent(){
        return eventQueue.poll();
    }

    public static <T extends Event> void addEvent(T event){
        eventQueue.add(event);
    }

    public static void clearQueue(){
        eventQueue.clear();
    }

}
