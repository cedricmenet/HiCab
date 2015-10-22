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
    var ws:WebSocket?

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
        print("You tapped at \(gestureRecognizer.locationInView(self.myDrawingView))")
        
        var mPoint:CGPoint =  gestureRecognizer.locationInView(self.myDrawingView)
        
        mPoint.x /= self.myDrawingView.bounds.width
        mPoint.y /= self.myDrawingView.bounds.height
        
        print("click : x\(mPoint.x), y \(mPoint.y) ")
        
        //best candidate on json
        
        var nearestStreet :JSON = []
        var bestDist:CGFloat = 1000000
        var bestD:CGPoint = CGPoint()
        var progression :CGFloat = 1
        var shouldreverse  : CGFloat = 1
        
        for (key,subJson):(String, JSON) in self.myJson["areas"][self.myDrawingView.mapId]["map"]["streets"] {
            
            
            var va = getVertexByName(subJson["path"][0].string!, vertices: self.myJson["areas"][self.myDrawingView.mapId]["map"]["vertices"])
            var vb = getVertexByName(subJson["path"][1].string!, vertices: self.myJson["areas"][self.myDrawingView.mapId]["map"]["vertices"])
            
            
            var a = CGPoint(
                x:CGFloat( va["x"].float!),
                y:CGFloat( va["y"].float!))
            
            var b = CGPoint(
                x:CGFloat( vb["x"].float!),
                y:CGFloat( vb["y"].float!))
            
            //on remet dans le bon ordre
            shouldreverse = 1
            if(a.x > b.x){
                var ptmp = a
                a = b
                b = ptmp
                shouldreverse = -1
            }
            
            var dist:CGFloat = 100000
            var c = mPoint
            var d : CGPoint = CGPoint()
            
            
            if(a.x == b.x){
                dist = abs ( a.x - c.x)
                d.x = a.x
                d.y = c.y
                
            }
            else if(a.y == b.y){
                dist = abs ( a.y -  c.y)
                d.x = c.x
                d.y = a.y
                print("test")
            }
            else{
                
                
                
                
                
                var v0 = (b.x-a.x)*(c.y-a.y)*(b.y-a.y)
                var v1 = c.x*pow(b.x-a.x,2)+a.x*pow(b.y-a.y,2)
                var v2 = (pow(b.x-a.x,2)+pow(b.y-a.y,2))
                
                d.x = (v0 + v1) / v2
                d.y = (b.y-a.y)/(b.x-a.x)*(d.x-a.x)+a.y
                
                 dist = sqrt(pow(c.x-d.x,2)+pow(c.y-d.y,2))
            }
            
            
            
            
            
            print("dist \(dist) d.x\(d.x), d.y \(d.y) ")
            
            if(((d.x >= a.x && d.x <= b.x) || (d.x <= a.x && d.x >= b.x) ) && ((d.y >= a.y && d.y <= b.y) || (d.y <= a.y && d.y >= b.y)))
            {
                    // on a le point D valide
                    // on cherche la distance entre D et C
                
                
                    
                    if(bestDist > dist){
                        
                        progression =  sqrt(pow(a.x-d.x,2)+pow(a.y-d.y,2)) / sqrt(pow(a.x-b.x,2)+pow(a.y-b.y,2))
                        if(shouldreverse == 1){
                            progression = 1 - progression
                        }
                        bestD = d
                        nearestStreet = subJson
                        bestDist = dist
                    }
            }
            
        }
        
        // a ce stade on a la meilleure Street
        
        print("bestD.x\(bestD.x), bestD.y \(bestD.y) ")
        print("nearestStreet\(nearestStreet)")

        var jname = nearestStreet["name"].string
        var jarea = nearestStreet["area"].string
        var jpath1 = nearestStreet["path"][0].string
        var jpath0 = nearestStreet["path"][1].string
        var joneway = nearestStreet["oneway"].bool
        
        let blop:String = "{\"location\": {\"backward\": false,\"name\": \"\(jname!)\",\"weight\": 1.0,\"area\": \"\(jarea!)\",\"loc_type\": \"street\",\"path\": [\"\(jpath0!)\",\"\(jpath1!)\"],\"oneway\": \(joneway!),\"progression\": \(progression),\"coord\": {\"y\": 1,\"x\": 0}}}"
        
        
        print(blop)
        
        
        
        self.ws!.send(blop)
        
        
        
        
        //let ,,valid = NSJSONSerialization.isValidJ,,SONObject(jsonObject) // true
        
        
        
        //self.ws!.send(msg)
        
        /*let alertController = UIAlertController(title: nil, message: "You tapped at \(gestureRecognizer.locationInView(self.myDrawingView))", preferredStyle: .Alert)
        alertController.addAction(UIAlertAction(title: "Dismiss", style: .Cancel, handler: { _ in }))
        self.presentViewController(alertController, animated: true, completion: nil)*/
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
                    self.ws = WebSocket("ws://192.168.1.1/\(self.channel)")
                    let send : ()->() = {
                        let msg = "\(++messageNum): \(NSDate().description)"
                        print("send: \(msg)")
                        self.ws!.send(msg)
                    }
                    self.ws!.event.open = {
                        print("opened")
                        //send()
                    }
                    self.ws!.event.close = { code, reason, clean in
                        print("close , \(code), \(reason)")
                        //self.myDrawingView.reloadData()
                    }
                    self.ws!.event.error = { error in
                        print("error \(error)")
                    }
                    self.ws!.event.message = { message in
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
    
    
    func getVertexByName(name:String,vertices:JSON) ->JSON
    {
        for (key,subJson):(String, JSON) in vertices{
            if(subJson["name"].string == name){
                return subJson
            }
        }
        return nil
    }
    

}

