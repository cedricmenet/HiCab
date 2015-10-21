//
//  DataViewController.swift
//  Projet 3A
//
//  Created by Projet 3A on 13/10/2015.
//  Copyright © 2015 Projet 3A. All rights reserved.
//

import UIKit

class DataViewController: UIViewController {

    @IBOutlet weak var dataLabel: UILabel!
    var dataObject: String = "BLOP" 


    override func viewDidLoad() {
        super.viewDidLoad()
        
        print("test")
        
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    override func viewWillAppear(animated: Bool) {
        super.viewWillAppear(animated)
        self.dataLabel!.text = dataObject
    }


}

