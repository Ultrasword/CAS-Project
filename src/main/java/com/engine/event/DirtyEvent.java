package com.engine.event;

public class DirtyEvent extends Event{
    private final static int eventID = 1;
    private int vboIndex;
    private long uid;

    public DirtyEvent(long uid, int vboIndex){
        super(eventID);
        this.vboIndex = vboIndex;
        this.uid = uid;
    }

    @Override
    public void handleEvent() {

    }
}
