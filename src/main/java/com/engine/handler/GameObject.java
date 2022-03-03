package com.engine.handler;

import com.engine.comp.Component;
import com.engine.event.DirtyEvent;
import com.engine.event.EventQueue;
import org.joml.Vector3f;

import java.util.HashMap;

public class GameObject {

    public static long id = 0;

    protected Vector3f position;
    protected HashMap<String, Component> components;
    private boolean inVBO, dirty;
    private int VBOindex;
    private long uid;

    public GameObject(){
        inVBO = false;
        components = new HashMap<>();
        uid = getID();
    }

    protected void update(float dt){
        for(String comp : components.keySet()){
            components.get(comp).update(dt);
        }
    }

    public <T extends Component> T getComponent(Class<T> componentClass){
        if (components.containsKey(componentClass.getName())){
            return componentClass.cast(components.get(componentClass.getName()));
        }else return null;
    }

    public <T extends Component> void removeComponent(Class<T> componentClass){
        components.remove(componentClass.getName());
    }

    public <T extends Component> void addComponent(T component){
        components.put(component.getClass().getName(), component);
    }

    public void checkIfDirty(){
        if(isInVBO())
            if(this.dirty){
                EventQueue.addEvent(new DirtyEvent(this.getUID(), this.getVBOindex()));
                dirty = false;
            }
    }

    protected boolean isDirty(){
        return this.dirty;
    }

    protected void notDirty(){
        this.dirty = false;
    }

    protected void Dirty(){
        this.dirty = true;
    }

    public boolean isInVBO(){
        return this.inVBO;
    }

    public void setInVBO(boolean is){
        inVBO = is;
    }

    public void setVBOindex(int i){
        this.VBOindex = i;
    }

    public int getVBOindex(){
        return this.VBOindex;
    }

    public static long getID(){
        return id++;
    }

    public long getUID(){
        return this.uid;
    }

}
