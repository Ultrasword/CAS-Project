package com.engine.handler;

import java.util.concurrent.ConcurrentHashMap;

public class EntityHandler {
    /* handles entities
        All it does is store them and update them
     */
    public final static int MAX_ENTITY_COUNT = 256;
    // TODO - implement entity limit per handler
    //  also batch handlers

    private ConcurrentHashMap<Long, GameObject> gameObjectMap;

    public EntityHandler(){
        gameObjectMap = new ConcurrentHashMap<>();
    }

    public void update(float dt){
        for(GameObject gameObject : gameObjectMap.values()){
            gameObject.update(dt);
            gameObject.checkIfDirty();
        }
    }

    public GameObject getGameObject(long uid){
        return gameObjectMap.get(uid);
    }

    public <T extends GameObject> void addGameObject(T object){
        gameObjectMap.put(object.getUID(), object);
    }

    public void clean(){
        this.gameObjectMap.clear();
    }

}
