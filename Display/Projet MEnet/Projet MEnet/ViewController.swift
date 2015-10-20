//
//  ViewController.swift
//  Projet MEnet
//
//  Created by Projet 3A on 19/10/2015.
//  Copyright © 2015 Projet 3A. All rights reserved.
//

import UIKit


protocol MyViewDelegate {
    func JsonMap() -> JSON;
}

class ViewController: UIViewController, MyViewDelegate{
    
    
    func JsonMap() -> JSON {
        return self.myJson
    }
    
    @IBOutlet weak var myDrawingView: MyDrawingView!
    var toPass:String = ""
    var myJson : JSON = []

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        print(toPass)
        
        
        myDrawingView.myViewDelegate = self
        self.view.addSubview(myDrawingView)
        
        
        let url : NSURL? = NSURL(string: "http://192.168.1.1/getmap")
        let session = NSURLSession.sharedSession()
        let dataTask = session.dataTaskWithURL((url)!, completionHandler: { (data: NSData?, response:NSURLResponse?,
            error: NSError?) -> Void in
            //do something
            print("hi")
            //print(NSString(data: data!, encoding: NSUTF8StringEncoding))
            
            
            if error != nil {
                print(error)
                // handle error
            }
            else{
                
                let data_str = NSString(data:data!, encoding:NSUTF8StringEncoding)
                if let dataFromString = data_str!.dataUsingEncoding(NSUTF8StringEncoding, allowLossyConversion: false) {
                    self.myJson = JSON(data: dataFromString)
                    //update model
                    self.myDrawingView.reloadData()
                    //print(self.myJson)
                }
            }
        })
        
        dataTask.resume()

        
        
        //echoTest()
    
        
        
        
    }
    
    override func viewWillAppear(animated: Bool) {
        myDrawingView.reloadData()
    }
    

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
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
            self.myDrawingView.reloadData()
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

