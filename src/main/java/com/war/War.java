package com.war;

import com.engine.event.EventHandlerPool;
import com.engine.hardware.Window;

public class War {

    public static void main(String[] args) {
        // EventHandlerPool eventHandler = EventHandlerPool.getInstance(2);
        Window window = Window.get();
        window.init();
    
        // eventHandler.start();
        window.loop();

//        try{
//            eventHandler.endThreads();
//        } catch (InterruptedException e) {
//            e.printStackTrace();
//            // just delete all threads from existnce
//            eventHandler.deleteFromExistence();
//        }
        window.end();
    }
}
