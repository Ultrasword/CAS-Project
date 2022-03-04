package com.engine.handler;


import java.util.Stack;

public class SceneHandler {

    // queue setup
    public static Stack<Scene> sceneStack = new Stack<>();
    public static Scene currentScene;

    public static <T extends Scene> void pushScene(T scene){
        sceneStack.push(scene);
        currentScene = scene;
        scene.start();
    }

    public static void update(float dt){
        currentScene.update(dt);
    }

    public static void render(){
        currentScene.render();
    }

    public static void clean(){
        for(Scene scene : sceneStack){
            scene.clean();
        }
        sceneStack.clear();
    }

}
