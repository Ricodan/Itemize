#!/usr/bin/env python3

import threading
import sys
import socket
import selectors
import types
import json

def enter_list_name(sock, data):
    # read user input
        if not data.outb:
            # read from user input
            data.outb = input("Enter name of list\n")
            data.list = data.outb
            # nu innhåller data.outb något så då skickar vi på socketen
        if data.outb:
            print("sending", str(data.outb), "to connection")
            sent = sock.send(data.outb.encode())  # Should be ready to write
            data.outb = data.outb[sent:]

def print_list(list):
    i=1
    for item in list:
        print(i, '.\t', item)
        i+=1

def get_list(sock, data):
    data.outb = 'show_list()'
    #if mask & selectors.EVENT_WRITE:
    if data.outb:
            print("sending", str(data.outb), "to connection")
            sent = sock.send(data.outb.encode())  # Should be ready to write
            data.sent_msgs += 1
            data.outb = data.outb[sent:]
            data.show=True

def service_connection(sock, data):
    #if mask & selectors.EVENT_READ:
        print('we are reading')
        print('data.show_all: ', data.show_all)
        print('data.show: ', data.show)
        print('data.add: ', data.add)
        print('data.delete: ', data.delete)
        if data.show:
            # receive json
            recv_data = sock.recv(1024)
            recv_data = json.loads(recv_data)
            print('Items in list ', data.list, ': \n')
            print_list(recv_data[data.list])
            data.show=False
            data.outb = input('Your input: ')
        elif data.show_all:
            recv_data = sock.recv(1024)
            recv_data = json.loads(recv_data)
            print('These are your lists:\n')
            print_list(recv_data)
            data.show_all = False
            data.show=True
            # get input from user
            data.outb = input('Type index of list to display: ')
            index = int(data.outb)-1
            data.list = recv_data[index]
            #if mask & selectors.EVENT_WRITE:
            if data.outb:
                    print("sending", str(data.outb), "to connection")
                    sent = sock.send(data.outb.encode())  # Should be ready to write
                    data.sent_msgs += 1
                    data.outb = data.outb[sent:]
        elif data.add:
            # receive json
            recv_data = sock.recv(1024)
            recv_data = json.loads(recv_data)
            print('Items in list ', data.list, ': \n')
            print_list(recv_data[data.list])
            data.add=False
            # get input from user
            while data.cont:
                data.outb = input('Item to add: ')
                #if mask & selectors.EVENT_WRITE:
                if data.outb:
                        print("sending", str(data.outb), "to connection")
                        sent = sock.send(data.outb.encode())  # Should be ready to write
                        data.sent_msgs += 1
                        data.outb = data.outb[sent:]
                answer = input('Add another item? (Y/N) ')
                if answer == 'N' or answer == 'n':
                    data.cont = False
            # now we want to get the finished list from server
            get_list(sock, data)
        elif data.delete:
            # receive json
            recv_data = sock.recv(1024)
            recv_data = json.loads(recv_data)
            print('Items in list ', data.list, ': \n')
            print_list(recv_data[data.list])
            data.delete = False
            # get input from user
            while data.cont:
                data.outb = input('Enter number of item to delete: ')
                #if mask & selectors.EVENT_WRITE:
                if data.outb:
                        print("sending", str(data.outb), "to connection")
                        sent = sock.send(data.outb.encode())  # Should be ready to write
                        data.sent_msgs += 1
                        data.outb = data.outb[sent:]
                answer = input('Delete another item? (Y/N) ')
                if answer == 'N' or answer == 'n':
                    data.cont = False
            # now we want to get the finished list from server
            get_list(sock, data)

        else:
            print('we are about to receive')
            recv_data = sock.recv(1024).decode()  # Should be ready to read
            print('we have just received')
            if recv_data:
                data.recv_total += 1
                print("received", str(recv_data), "from connection")
                if recv_data == 'Enter name of list: ':
                    # go to function enter_list_name
                    enter_list_name(sock, data)
                elif recv_data == "Press 'a' to add items to list\nPress 'd' to delete items from list":
                    # now we will send a character to server and receive json object back
                    data.outb = input('Your input: ')
                    if data.outb == 'a':
                        data.cont=True
                        data.add=True
                    else:
                        data.cont=True
                        data.delete=True
                elif not data.recv_total == 1 and not data.sent_msgs == 0:
                    # if we want input from user
                    data.outb = input('Your input: ')
                    if data.outb == 'show_lists()':
                        data.show_all=True
                        print('setting data.show_all to ', data.show_all)
    #if mask & selectors.EVENT_WRITE:
        if data.recv_total == 1 and data.sent_msgs == 0:
            # read from user input
            data.outb = input("Enter your function\n")
            # nu innhåller data.outb något så då skickar vi på socketen
        #if not data.outb:
            # read from user input
            #data.outb = input("Enter your function\n")
            # nu innehåller data.outb något så då skickar vi på socketen
        if data.outb:
            print("sending", str(data.outb), "to connection")
            sent = sock.send(data.outb.encode())  # Should be ready to write
            data.sent_msgs += 1
            data.outb = data.outb[sent:]