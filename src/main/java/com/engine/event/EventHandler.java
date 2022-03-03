package com.engine.event;

public class EventHandler implements Runnable{

    public Thread thread;
    private String name;
    private boolean running;

    public EventHandler(String name){
        this.name = name;
    }

    public EventHandler(int name){
        this.name = Integer.toString(name);
        this.running = false;
    }

    public void start(){
        this.thread = new Thread(name);
        this.running = true;
    }

    @Override
    public void run() {

        while (running){
            // get task from event queue
            Event event = EventQueue.getEvent();
            if (event.type == 0)
                running = false;
            else event.handleEvent();

            // sleep thread for half a second
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    public void terminate(){
        this.running = false;
        // absolutely deleted >:D
        this.thread.interrupt();
    }

}
