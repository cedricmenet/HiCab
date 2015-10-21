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
    func JsonCab() -> JSON;
}

class ViewController: UIViewController, MyViewDelegate{
    
    
    func JsonMap() -> JSON {
        return self.myJson
    }
    func JsonCab() -> JSON {
        return self.myCab
    }
    
    
    @IBOutlet weak var myDrawingView: MyDrawingView!
    var toPass:String = ""
    var myJson : JSON = []
    var myCab : JSON = []
    var channel:String = ""

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        print(toPass)
        
        
        myDrawingView.myViewDelegate = self
        if(toPass.isEmpty){
            myDrawingView.mapId = 0

        }
        else{
            myDrawingView.mapId = IntegerLiteralType( toPass)!

        }
                self.view.addSubview(myDrawingView)
        
        
        //tap gesture recogniser
        
        
        let gestureRecognizer = UITapGestureRecognizer(target: self, action: "handleTap:")
        self.myDrawingView.addGestureRecognizer(gestureRecognizer)
        
        
        
        
        
        
        
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

        
        
        startWs()
    
        
        
        
    }
    
    func handleTap(gestureRecognizer: UIGestureRecognizer) {
        
        
        
        
        let alertController = UIAlertController(title: nil, message: "You tapped at \(gestureRecognizer.locationInView(self.myDrawingView))", preferredStyle: .Alert)
        alertController.addAction(UIAlertAction(title: "Dismiss", style: .Cancel, handler: { _ in }))
        self.presentViewController(alertController, animated: true, completion: nil)
    }
    
    
    
    override func viewWillAppear(animated: Bool) {
        myDrawingView.reloadData()
    }
    

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
    
    func startWs(){
        
        
        let url : NSURL? = NSURL(string: "http://192.168.1.1/subscribe/display")
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
                    let channelJSON = JSON(data: dataFromString)
                    self.channel = channelJSON["channel"].string!
                    
                    
                    
                    print("channel : \(self.channel)")
                    
                    
                    var messageNum = 0
                    let ws = WebSocket("ws://192.168.1.1/\(self.channel)")
                    let send : ()->() = {
                        let msg = "\(++messageNum): \(NSDate().description)"
                        print("send: \(msg)")
                        ws.send(msg)
                    }
                    ws.event.open = {
                        print("opened")
                        //send()
                    }
                    ws.event.close = { code, reason, clean in
                        print("close , \(code), \(reason)")
                        //self.myDrawingView.reloadData()
                    }
                    ws.event.error = { error in
                        print("error \(error)")
                    }
                    ws.event.message = { message in
                        if let text = message as? String {
                            //print("recv: \(text)")
                            
                            let dataFromString = text.dataUsingEncoding(NSUTF8StringEncoding, allowLossyConversion: false)
                            self.myCab = JSON(data: dataFromString!)
                            
                            self.myDrawingView.updateCab()
                            
                            if messageNum == 10 {
                                //ws.close()
                            } else {
                                //send()
                            }
                        }
                    }
                }
            }
        })
        
        dataTask.resume()
        
        
        
    }
    
    
    
    

    


}

