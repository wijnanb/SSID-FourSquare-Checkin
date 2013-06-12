//
//  ViewController.m
//  SSID-FourSquare-Checkin
//
//  Created by Bert Wijnants on 12/06/13.
//  Copyright (c) 2013 Mobile Vikings. All rights reserved.
//

#import "ViewController.h"
#import <SystemConfiguration/CaptiveNetwork.h>

@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad
{
    [super viewDidLoad];
	// Do any additional setup after loading the view, typically from a nib.
    
    NSLog(@"finding your SSID");
    CFArrayRef myArray1 = CNCopySupportedInterfaces();
    CFDictionaryRef myDict = CNCopyCurrentNetworkInfo(CFArrayGetValueAtIndex(myArray1, 0));
    NSLog(@"%@",myDict);
    
    NSDictionary* ssid_info = (__bridge NSDictionary*) myDict;
    NSString* SSID = [ssid_info objectForKey:@"SSID"];
    NSLog(@"%@", SSID);
    
    [[self labelSSID] setText:SSID];
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

@end
