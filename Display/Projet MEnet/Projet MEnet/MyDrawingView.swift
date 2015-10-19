//
//  MyDrawingView.swift
//  Projet MEnet
//
//  Created by Projet 3A on 19/10/2015.
//  Copyright © 2015 Projet 3A. All rights reserved.
//

import UIKit

class MyDrawingView: UIView {

    
    // Only override drawRect: if you perform custom drawing.
    // An empty implementation adversely affects performance during animation.
    
    
    override func drawRect(rect: CGRect) {
        // Drawing code
        
        let h = rect.height
        let w = rect.width
        let color:UIColor = UIColor.yellowColor()
        
        let drect = CGRect(x: (w * 0.25),y: (h * 0.25),width: (w * 0.5),height: (h * 0.5))
        let bpath:UIBezierPath = UIBezierPath(rect: drect)
        
        color.set()
        bpath.stroke()
        
        NSLog("drawRect has updated the view")
        echoTest()
    }
    
    
    func echoTest(){
        var messageNum = 0
        let ws = WebSocket("wss://echo.websocket.org")
        let send : ()->() = {
            let msg = "\(++messageNum): \(NSDate().description)"
            print("send: \(msg)")
            ws.send(msg)
        }
        ws.event.open = {
            print("opened")
            send()
        }
        ws.event.close = { code, reason, clean in
            print("close")
        }
        ws.event.error = { error in
            print("error \(error)")
        }
        ws.event.message = { message in
            if let text = message as? String {
                print("recv: \(text)")
                if messageNum == 10 {
                    ws.close()
                } else {
                    send()
                }
            }
        }
    }

}
