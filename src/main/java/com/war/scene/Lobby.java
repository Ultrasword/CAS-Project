package com.war.scene;

import com.engine.Camera;
import com.engine.comp.Sprite;
import com.engine.comp.SpriteRenderer;
import com.engine.comp.Testing;
import com.engine.graphics.Renderer;
import com.engine.graphics.SpriteSheet;
import com.engine.graphics.VBOs.GameEntity2DVBO;
import com.engine.handler.Entities.GameEntity2D;
import com.engine.handler.EntityHandler;
import com.engine.handler.Scene;
import com.engine.handler.Transform2D;
import com.engine.hardware.KeyListener;
import com.engine.hardware.MouseListener;
import com.engine.hardware.Window;
import com.engine.utils.Time;
import org.joml.Vector2f;
import org.joml.Vector3f;

import static org.lwjgl.glfw.GLFW.*;

public class Lobby extends Scene {

    float t = 0;

    public Lobby() {
        // set up scene
        this.entityHandler = new EntityHandler();
        this.renderer = new Renderer();
        this.renderer.addVBO(new GameEntity2DVBO(null));

        // create camera
        this.camera = new Camera(1280f, 720f, new Vector3f(0, 0, -10),
                1f, -.1f, 100f, 60f);
        this.camera.setRotation(.5f, 1, 0);
        this.camera.adjustOrthoProjection();
    }

    public void start(){
        // nothing exists sadge
        // add objects
        SpriteSheet spriteSheet = new SpriteSheet("assets/animations/warrior/warrior_attack.png", 64, 64, 20, 0, 0, 0);
        for(int i = 0; i < 5; i++){
            for (int j = 0; j < 4; j++){
                GameEntity2D entity2D = new GameEntity2D(new Transform2D(new Vector3f(i*100, j * 100, 0), new Vector2f(100, 100), 10 * i + j * 10));
                entity2D.addComponent(new SpriteRenderer(spriteSheet.getSprite(j * 4 + i)));
                entity2D.addComponent(new Testing());
                addGameObject(entity2D);
            }
        }
        MouseListener.startInput();
        Time.start();
    }

    @Override
    public void update(float dt) {
        if (KeyListener.isKeyPressed(GLFW_KEY_A))
            camera.move(-10.f, 0.0f, 0.0f);
        if (KeyListener.isKeyPressed(GLFW_KEY_D))
            camera.move(10.0f, 0.0f, 0.0f);
        if (KeyListener.isKeyPressed(GLFW_KEY_W))
            camera.move(0.0f, 10.0f, 0.0f);
        if (KeyListener.isKeyPressed(GLFW_KEY_S))
            camera.move(0.0f, -10.0f, 0.0f);
        if (KeyListener.isKeyPressed(GLFW_KEY_K))
            removeGameObject(0,0, 1);

        this.camera.update();

        entityHandler.update(Time.deltaTime);
    }

    @Override
    public void render() {
        renderer.renderArrays();
        MouseListener.endFrame();
    }
}
