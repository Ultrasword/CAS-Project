package com.engine.event;

public class EventHandler implements Runnable {

    private String name;
    private boolean running;
    private Thread thread;

    public EventHandler(String name){
        this.name = name;
    }

    public EventHandler(int name){
        this.name = Integer.toString(name);
    }

    public void start(){
        this.running = true;
        this.thread = new Thread(this, this.name);
        this.thread.start();
    }

    @Override
    public void run() {
        try {
            while (this.running) {
                // get task from event queue
                Event event = EventQueue.getEvent();
                if (event != null) {
                    if (event.type == 0)
                        this.running = false;
                    else {
                        event.handleEvent();
                        System.out.println("EVENTHANDLER (EventHandler.java): Handled " + event.getClass().getName());
                    }
                }
                // System.out.println("Running thread " + this.getName());

                // sleep thread for quarter second
                Thread.currentThread().sleep(250);
            }
        } catch (InterruptedException e) {
            System.out.println("Ending process " + this.getName());
        }
    }

    public void join(long time) throws InterruptedException {
        this.thread.join(time);
        System.out.println("Joining process " + this.getName());
    }

    public void terminate(){
        this.running = false;
        Thread.currentThread().interrupt();
        System.out.println("Deleting process " + this.getName());
    }

    public String getName() {
        return name;
    }

    public boolean isRunning() {
        return running;
    }

    public Thread getThread() {
        return thread;
    }
}
