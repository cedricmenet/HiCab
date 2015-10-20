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
    var mapJSON: JSON?
    
    
    func reloadData(){
        if myViewDelegate != nil {
            mapJSON = myViewDelegate!.JsonMap()
            print(mapJSON)
        }
        self.setNeedsDisplay()
    }
    
    
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
        
        
    }
    
    
    
    

}
