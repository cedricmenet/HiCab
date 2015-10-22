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
    
    var myViewDelegate : MyViewDelegate?
    var mapJSON: JSON = []
    var cabJSON: JSON = []
    
    var mapId:IntegerLiteralType = 0
    
    
    func reloadData(){
        if myViewDelegate != nil {
            mapJSON = myViewDelegate!.JsonMap()
            
        }
        
        dispatch_async(dispatch_get_main_queue()) {
            self.setNeedsDisplay()
        }
    }
    
    func updateCab(){
        if myViewDelegate != nil {
            cabJSON = myViewDelegate!.JsonCab()
        }
        
        dispatch_async(dispatch_get_main_queue()) {
            self.setNeedsDisplay()
        }
    }
    
    
    override func drawRect(rect: CGRect) {
        // Drawing code
        /*
        let h = rect.height
        let w = rect.width
        let color:UIColor = UIColor.yellowColor()
        */var drect:CGRect

        
        /*for street in mapJSON["areas"][0]["map"]["streets"] {
            
            if(street["path"].count == 2 ){
                
            }
            
        }*/
        
        
        for (key,subJson):(String, JSON) in mapJSON["areas"][mapId]["map"]["streets"] {
            //Do something you want
            
            //dessin des rues
            let vertexA = getVertexByName(subJson["path"][0].string!, vertices: mapJSON["areas"][mapId]["map"]["vertices"])
            let vertexB = getVertexByName(subJson["path"][1].string!, vertices: mapJSON["areas"][mapId]["map"]["vertices"])
            
            print("vertexA")
            print(vertexA)
            
            let plusPath = UIBezierPath()
            
            plusPath.lineWidth = 3
            plusPath.moveToPoint(CGPoint(
                x:CGFloat( vertexA["x"].float!)*bounds.width,
                y:CGFloat( vertexA["y"].float!)*bounds.height))
            
            plusPath.addLineToPoint(CGPoint(
                x:CGFloat( vertexB["x"].float!)*bounds.width,
                y:CGFloat( vertexB["y"].float!)*bounds.height))
            UIColor.blueColor().setStroke()
            plusPath.stroke()
            
            
            
            print(key)
            print(subJson)
            print("lol")
            
            
        }
        for (key,subJson):(String, JSON) in mapJSON["areas"][mapId]["map"]["vertices"] {
            
            
            let fieldFont = UIFont(name: "Helvetica Neue", size: 18)
            let fieldColor: UIColor = UIColor.darkGrayColor()
            let paraStyle = NSMutableParagraphStyle()
            let skew = 0.1
            paraStyle.alignment = NSTextAlignment.Center
            
            
            
            let attributes: NSDictionary = [
                NSForegroundColorAttributeName: fieldColor,
                NSParagraphStyleAttributeName: paraStyle,
                NSObliquenessAttributeName: skew,
                NSFontAttributeName: fieldFont!
            ]
            
            let s: NSString = subJson["name"].string!
            
            let x = CGFloat( subJson["x"].float!)*bounds.width
            let y = CGFloat( subJson["y"].float!)*bounds.height
            
            drect = CGRectMake(x-25, y-25, 50, 50)
            let path = UIBezierPath(ovalInRect: drect)
            UIColor.greenColor().setFill()
            path.fill()
            
            
            
            s.drawInRect(drect, withAttributes: attributes as? [String : AnyObject])
            //Do something you want
            
            
            
        }
        
        if(cabJSON != nil){
            for (key,subJson):(String, JSON) in cabJSON["cab_infos"] {
                print(subJson)
                let test = subJson["location"]["area"].string == mapJSON["areas"][mapId]["name"].string
                
                let a1 = subJson["location"]["area"].string
                let a2 = mapJSON["areas"][mapId]["name"].string
                print("area check\(test), \(a1),\(a2)")
                
                if(subJson["location"]["area"].string == mapJSON["areas"][mapId]["name"].string){
                    let x = CGFloat( subJson["location"]["coord"]["x"].float!)*bounds.width
                    let y = CGFloat( subJson["location"]["coord"]["y"].float!)*bounds.height
                    
                    
                    let fieldFont = UIFont(name: "Helvetica Neue", size: 18)
                    let fieldColor: UIColor = UIColor.darkGrayColor()
                    let paraStyle = NSMutableParagraphStyle()
                    let skew = 0.1
                    paraStyle.alignment = NSTextAlignment.Center
                    
                    
                    
                    let attributes: NSDictionary = [
                        NSForegroundColorAttributeName: fieldColor,
                        NSParagraphStyleAttributeName: paraStyle,
                        NSObliquenessAttributeName: skew,
                        NSFontAttributeName: fieldFont!
                    ]
                    
                    drect = CGRectMake(x-10, y-10, 20, 20)
                    
                    
                    let tmp: NSNumber = subJson["id_cab"].number!
                    let s: NSString = tmp.stringValue
                    let path = UIBezierPath(ovalInRect: drect)
                    UIColor.lightGrayColor().setFill()
                    path.fill()
                    s.drawInRect(drect, withAttributes: attributes as? [String : AnyObject])
                    
                    
                }
            }

        }
        
        
        
        
        //iterate on vertex
        /*for vertex in mapJSON["areas"][0]["map"]["vertices"] {
        
        }*/
        
        
        /*if(mapJSON["areas"][0]["map"]["vertices"][0]["name"].string != "m"){
            drect = CGRect(x: (w * 0.5),y: (h * 0.25),width: (w * 0.5),height: (h * 0.5))
            let path = UIBezierPath(ovalInRect: drect)
            UIColor.greenColor().setFill()
            path.fill()
            
            
            let plusHeight: CGFloat = 3.0
            let plusWidth: CGFloat = min(bounds.width, bounds.height) * 0.6
            
            //create the path
            let plusPath = UIBezierPath()
            
            //set the path's line width to the height of the stroke
            plusPath.lineWidth = plusHeight
            
            //move the initial point of the path
            //to the start of the horizontal stroke
            plusPath.moveToPoint(CGPoint(
                x:bounds.width/2 - plusWidth/2,
                y:bounds.height/2))
            
            //add a point to the path at the end of the stroke
            plusPath.addLineToPoint(CGPoint(
                x:bounds.width/2 + plusWidth/2,
                y:bounds.height/2))
            
            //set the stroke color
            UIColor.whiteColor().setStroke()
            
            //draw the stroke
            plusPath.stroke()
            
            
            
            
            
        }
        else{
            
            drect = CGRect(x: (w * 0.25),y: (h * 0.25),width: (w * 0.5),height: (h * 0.5))
        }
        
        let bpath:UIBezierPath = UIBezierPath(rect: drect)
        
        color.set()
        bpath.stroke()*/
        
        NSLog("drawRect has updated the view")
        
        
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
