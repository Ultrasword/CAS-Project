package com.war;

import com.engine.event.EventHandler;
import com.engine.event.EventHandlerPool;
import com.engine.handler.SceneHandler;
import com.engine.hardware.Window;
import com.war.scene.Lobby;

public class War {
    public static void init(){
        SceneHandler.pushScene(new Lobby());
    }

    public static void main(String[] args) {

        EventHandlerPool eventHandler = EventHandlerPool.getInstance(2);
        eventHandler.start();

        Window window = Window.get();
        window.init();

        // add stuff

        try {
            init();
            window.loop();
        } catch (Exception e) {
            e.printStackTrace();
        }
        SceneHandler.clean();
        window.end();
        try{
            eventHandler.endThreads(2000);
            Thread.sleep(2000);
            System.out.println("Deleting everything");
            for(EventHandler e : eventHandler.getThreads()){
                if (e.getThread().isAlive()){
                    new InterruptedException();
                }
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
            // just delete all threads from existnce
            eventHandler.deleteFromExistence();
        }
    }

}
