//
//  FirstViewController.swift
//  Projet MEnet
//
//  Created by Projet 3A on 20/10/2015.
//  Copyright © 2015 Projet 3A. All rights reserved.
//

import UIKit

class FirstViewController: UIViewController,UITextFieldDelegate {
    
    @IBOutlet weak var IDMapTextField: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        IDMapTextField.delegate = self
        IDMapTextField.keyboardType = UIKeyboardType.NumberPad
        
        
        
    }
    
    func textField(textField: UITextField,
        shouldChangeCharactersInRange range: NSRange,
        replacementString string: String)
        -> Bool
    {
        // We ignore any change that doesn't add characters to the text field.
        // These changes are things like character deletions and cuts, as well
        // as moving the insertion point.
        //
        // We still return true to allow the change to take place.
        if string.characters.count == 0 {
            return true
        }
        
        // Check to see if the text field's contents still fit the constraints
        // with the new content added to it.
        // If the contents still fit the constraints, allow the change
        // by returning true; otherwise disallow the change by returning false.
        let currentText = textField.text ?? ""
        let prospectiveText = (currentText as NSString).stringByReplacingCharactersInRange(range, withString: string)
        
       
            
        
            // Allow only digits in this field,
            // and limit its contents to a maximum of 3 characters.
        
            return containsOnlyCharactersIn("0123456789",Mystring: prospectiveText) && prospectiveText.characters.count <= 3
            
        
    }
    func containsOnlyCharactersIn(matchCharacters: String, Mystring: String) -> Bool {
        let disallowedCharacterSet = NSCharacterSet(charactersInString: matchCharacters).invertedSet
        return Mystring.rangeOfCharacterFromSet(disallowedCharacterSet) == nil
    }
    
    
    
    
    // Tap outside a text field to dismiss the keyboard
    // ------------------------------------------------
    // By changing the underlying class of the view from UIView to UIControl,
    // the view can respond to events, including Touch Down, which is
    // wired to this method.
    @IBAction func userTappedBackground(sender: AnyObject) {
        view.endEditing(true)
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject!) {
        if (segue.identifier == "testSegue") {
            var svc = segue.destinationViewController as! ViewController;
            
            svc.toPass = IDMapTextField.text!
            
        }
    }
    
    
    

}
