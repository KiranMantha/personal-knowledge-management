---
title: "Creating a Blockchain with Javascript"
url: https://medium.com/p/16e9dbdda691
---

# Creating a Blockchain with Javascript

[Original](https://medium.com/p/16e9dbdda691)

# Creating A Blockchain with Javascript

[![Valkyrie Holmes](https://miro.medium.com/v2/resize:fill:64:64/1*itdzTwERsItzQZ8RNbcDmA.jpeg)](/@vholmes113?source=post_page---byline--16e9dbdda691---------------------------------------)

[Valkyrie Holmes](/@vholmes113?source=post_page---byline--16e9dbdda691---------------------------------------)

7 min read

·

Apr 23, 2021

--

4

Listen

Share

More

A Simply Explained Replicate

> By Valkyrie Holmes

![]()

**This pretty much sums up the last five days of work for me.**

I decided to do something that I’ve never fully done before and that’s **trying to code in Javascript.** I’m only slightly familiar with Python and can’t say I’m even intermediate at that so this was definitely a fun challenge that had me pulling my hair out halfway through but also jumping for joy when the code finally worked the way I wanted it to. I get the struggle.

I’ve recently been learning about blockchain, **a system of decentralized currency that allows everyone to see every transaction that takes place and encode specific information**. That information, in this case, coins, are contained within blocks that are mined for more rewards, and rewards can be accessed by using specific keys to unlock the network. For more information on what blockchain is and the future of crypto, check out my other [article](https://vholmes113.medium.com/cryptocurrency-is-transforming-society-into-the-next-star-wars-738fc6301a18)!

But today, we’re discussing Javascript and **how I managed to write over 150 lines of code from scratch for a simple blockchain mechanism.**

You can watch this introductory video for a general rundown of my project:

I followed a series of videos from **Simply Explained**, a Youtube channel dedicated to learning new things in everything from coding to existential questions. He released a five-part playlist for coding your own blockchain in javascript. Although the videos didn’t tell me how to check if I had enough funds to make a transaction or how to communicate with other miners, it did give me a relatively simple overview of how the system works within a cryptocurrency like Bitcoin, for example.

## Creating the Base

My [first task](https://www.youtube.com/watch?v=zVqczFZr124&list=PLzvRQMJ9HDiTqZmbtFisdXFxul5k0F-Q4) was creating the actual chain itself. I used Visual Studio Code and a node.js extension that held all of the properties associated with building cryptocurrency. Once all that was installed, I went to work on my first page.

I defined the class “Block” and used a constructor **to receive the properties of the block**, that being the index, timestamp, data, and previous hash. The index tells us where the block sits on the chain, the timestamp tells us when it was created, the data would be the virtual code, and the previous hash contains the hash of the last block we cracked in the chain.

From there, we put the crypto.js file to good use by using the SHA256 library for different random hashes in our blocks. I stringified them, **which turns them into visible data**, and finished the block!

![]()

Next, I **created a new class** called Blockchain. Within this class is the code for the start of the chain, the genesis block, that contains a date, name, and index. I also input a “getLatestBlock” function that **returns the next block** to us as well as an “addBlock” function that **continues the chain**. With this, we needed to change the hash in accordance with the new blocks. In reality, you have to go through numerous checks before you can actually create another block but for these purposes, it’s been simplified.

Finally, I set up a variable called “valkyrieCoin” (very original, I know) to **correspond with the new class Blockchain** and created two new blocks which returned the series of blocks once I ran the program. It contains the property chain which contains hashes that reference the previous blocks. But there’s a problem, you can’t verify the integrity of the chain like this. This is why we then create a chain validation function **that can actually check whether or not a block is correct or not.**

![]()

![]()

## Proof of Work Mechanism

Alright, now that we’ve gotten all the basics out of the way, there are a few add-ons that can complete our blockchain a bit more. Right now we can create a new block quickly but we don’t have any security mechanism in place. That’s why we implement a [Proof of Work system](https://www.youtube.com/watch?v=HneatE69814&list=PLzvRQMJ9HDiTqZmbtFisdXFxul5k0F-Q4&index=2), set **to compensate for modern computing power and inflation of said coins.**

The first thing we need to do is set up a “mineBlock” feature with a set difficulty. This segment is contained within a “while loop” substring. The difficulty **sets up the hash so that a certain amount of zeros is added to the front**. The computer trying to mine the block then has to go through this added level of security, making the process much slower with your average laptop or PC. Once this is set, you create a nonce value that has the capability of ending the loop. With a few more tweaks, we can now test the code.

![]()

![]()

As you can see, the hashes of all of the blocks now start with 2 zeros and if we were to set the difficulty to 4, it would take a lot longer for the computer to mine the blocks and return back their hashes.

## Coin Incentives

Then we have the age-old question: why would people mine the blocks in the first place? Well, **digital currency of course**! But as of right now, we don’t have any set in place. So the next step was to [introduce virtual coins and transactions](https://www.youtube.com/watch?v=fRV6cGXVQ4I&list=PLzvRQMJ9HDiTqZmbtFisdXFxul5k0F-Q4&index=3) into the code.

I modified the code a bit to contain transactions in our Block class and also create a completely separate class for transactions. This class contains the “to address”, “from address”, and the amount that’s being transferred. Then, we create a “pending transactions” space where the crypto can live until the block is mined (kind of **like holding funds in a separate account**).

I also created a **mining reward** for each block that is transferred after the pending transactions action has been carried out (once the coins are successfully delivered to a set location). After setting up another validation mechanism to make sure nothing has been tampered with, **the balance is returned to the set address**. Our new balance is 100 from the mining rewards!

![]()

![]()

## Signing Transactions

Okay, we’re in the home stretch now. Now we have to solve the problem of [transaction security](https://www.youtube.com/watch?v=kWQ84S13-hw&list=PLzvRQMJ9HDiTqZmbtFisdXFxul5k0F-Q4&index=4). We have validation set in place, we have a mechanism, but now people can actually spend coins that aren’t even theirs because there’s no protection for those accounts. This is why we have to **use public and private keys for our accounts to sign off on each transaction**.

I cleaned up the code a little bit by putting them on different pages and now, we’re ready to sprint to the finish line!

I needed to import an **“elliptic” library with methods to verify signatures and create protected transactions** (specifically secp256k1) with public and private keys as “hex” strings. After storing those on another page, I could engineer the “calculateHash” code to be signed with every run-through. Before signing a transaction, I created the signature data that corresponds with certain hashes and worked in one more validation system to check whether or not the conditions have been met.

![]()

![]()

To run the code, I copied the private key into the const function to get the content of that wallet and then assigned a transaction of 10 coins to a random address (ideally, another person you’re trying to send coins to). As you can see, the balance is 90. This is because we had the mining reward of 100 from the block and we transferred 10 of those coins to another address.

![]()

Whew, that was a HUGE coding dump on you. Don’t feel bad if you didn’t understand everything, it took me quite a while to wrap my head around the different functions and why my code wasn’t working for the fiftieth time. All in all, it was quite fulfilling to see that final 90 pop up on my computer screen.

In the future, I plan on fully completing the series and building an angular frontend to my application but for time's sake and being able to fully explain how blockchain works, I figured that getting my foot in the door with some of the coding mechanisms was the best way to put my knowledge to good use. I want to continue this blockchain discovery and can’t wait to learn more.

Press enter or click to view image in full size

![]()

If you have any questions or concerns, feel free to email me at vholmes113@gmail.com.