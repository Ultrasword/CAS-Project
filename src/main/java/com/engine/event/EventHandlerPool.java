package com.engine.event;

public class EventHandlerPool {

    public static EventHandlerPool instance;

    private int threadCount;
    private EventHandler[] threads;

    public EventHandlerPool(int threads){
        this.threadCount = threads;
        this.threads = new EventHandler[threads];
        for (int i = 0; i < threads; i++)
            this.threads[i] = new EventHandler(i);
    }

    public void start(){
        for(int i = 0; i < this.threadCount; i++) {
            this.threads[i].start();
        }
    }

    public void endThreads(long time) throws InterruptedException {
        // clear queue
        EventQueue.clearQueue();
        // add events
        for(int i = 0; i < this.threadCount; i++)
            // the idea is to upload some thread end tasks
            EventQueue.addEvent(new EndThread());
        for(int i = 0; i < this.threadCount; i++){
            this.threads[i].join(time);
        }
    }

    public void deleteFromExistence(){
        // clear queue
        EventQueue.clearQueue();
        // kill them all
        for(int i = 0; i < this.threadCount; i++){
            this.threads[i].terminate();
        }
    }

    public static EventHandlerPool getInstance(int threadCount) {
        if(instance == null && threadCount != 0)
            instance = new EventHandlerPool(threadCount);
        else if (threadCount == 0)
            return null;
        return instance;
    }

    public int getThreadCount() {
        return threadCount;
    }

    public EventHandler[] getThreads() {
        return threads;
    }
}
