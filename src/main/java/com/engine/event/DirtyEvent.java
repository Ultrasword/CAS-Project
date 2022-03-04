package com.engine.event;

import com.engine.handler.SceneHandler;

public class DirtyEvent extends Event{
    private final static int eventID = 1;
    private int vboIndex;
    private long uid;

    public DirtyEvent(long uid, int vboIndex){
        super(eventID);
        this.vboIndex = vboIndex;
        this.uid = uid;
        System.out.println("Added dirty event");
    }

    @Override
    public void handleEvent() {
        // add to the renderer
        System.out.println("Dirty boi");
        SceneHandler.currentScene.getRenderer().getVboArray().get(vboIndex).addDirtySprite(SceneHandler.currentScene.getEntityHandler().getGameObject(uid));
    }
}
