---
title: "How I Made a Profit Mining Ethereum on AWS"
url: https://medium.com/p/2ffe3aab579
---

# How I Made a Profit Mining Ethereum on AWS

[Original](https://medium.com/p/2ffe3aab579)

# How I Made a Profit Mining Ethereum on AWS

## Is the game really worth playing?

[![James Robinson](https://miro.medium.com/v2/resize:fill:64:64/1*4T8NOPMOgtRGAW4DdXUNUg.jpeg)](/@jamesjessian?source=post_page---byline--2ffe3aab579---------------------------------------)

[James Robinson](/@jamesjessian?source=post_page---byline--2ffe3aab579---------------------------------------)

8 min read

·

Oct 23, 2021

--

19

Listen

Share

More

Press enter or click to view image in full size

![]()

I just wanted to put it out there that:

* It is possible
* AWS doesn’t ban you for mining on their servers
* It’s only profitable at certain times

It is certainly possible, and I managed it with fluky timing and a bit of tweaking. I didn’t expect it to be profitable at all. I was only experimenting to learn more about mining and try something new. Michael Ludvig [published an excellent article](https://michael-ludvig.medium.com/mining-bitcoin-and-other-crypto-on-aws-eb172940059f) documenting a setup for running `ethminer`on AWS GPU spot instances (temporary cheap servers) and I wanted to just give it a go and learn a few things.

I happened to run this on the 8th May 2021 which (I later learned) was the start of the best few days for Ethereum mining profitability in history. I launched the [CloudFormation template](https://github.com/mludvig/aws-ethereum-miner) (that Michael Ludvig had created) in the Ohio AWS region using the recommended g4dn.xlarge instance type.

The steps to do this are roughly:

* Create an AWS account
* Create an Ethereum wallet
* Upload the CloudFormation template
* Enter your Ethereum wallet public address (to receive all that Ether)

By the way, creating an Ethereum wallet is a lot simpler than a lot of websites make it out to be. You don’t need to sign up to *CryptoWalletExchangeBase* and upload your identity and wave on webcam to a robot. A “wallet” can be boiled down to just a public address and private key like this:

**public address**:   
`0x6672b0A9e258b6323450156fd5582ea112fb39C2`  
You can give this out to anybody. Ether can be sent to this address.

**private key**: `cb1b8e05e47f4d88de19ad4cc7abe16abba67c3c85586158de0266c6b4a99`  
(Never share your private key)  
This can be used to access the Ether held in the wallet. So you probably want to keep this one to yourself.

…and you can generate these yourself. For example:

The important things are to make sure you don’t lose them and to make sure no one else knows what the private key is. So run that code on a non-internet-connected Palm Pilot, store them on an encrypted floppy disk and then burn the evidence.

On the first mining attempt, I had the system running for a while and the AWS EC2 Spot Instances (cheap servers) ran for a combined total of 134.658 hours and I racked up 0.00485 Ether which (at the time) was worth about $19.

You can see how much you’ve earned by looking up your public wallet address on Ethermine: <https://ethermine.org/miners/your_public_address/dashboard>

Press enter or click to view image in full size

![]()

Here’s a snapshot of my AWS bill at the time:

Press enter or click to view image in full size

![]()

So no profit yet, but not as far off as I was expecting.

I was concerned there might be additional cost for the AutoScalingGroup that is used in the CloudFormation template, but that is free; you only have to pay for the AWS resources needed to run the application. But what I did notice was that several of the instances either crashed, were stuck at 0 MH/s, or just 10–20MH/s rather than running at the optimal 25.43 MH/s that others managed.

*Maybe the system would do better if there was something in place to automatically terminate instances that were not performing adequately.*

I checked a profit calculator. If these AWS EC2 Spot Instances run at 0.1578 per hour, and I was achieving the 25.43 MH/s that most of them were achieved, then all the lights were green.

Press enter or click to view image in full size

![]()

Working out exactly why some instances failed and some didn’t did not fit into the scope of this “pissing about with Ethereum” so I hacked something together. I decided to write some code to SSH into the EC2 Spot Instances to check for errors or a low hash rate. I created a KeyPair in AWS, downloaded it, and added a parameter to the CloudFormation template so that I could specify the name of this KeyPair and ensure it gets used by the spot instance Launch Template.

```
Parameters:  
  ...  
  KeyPairName:  
    Description: Name of EC2 key pair assigned to instances.  
    Type: String...LaunchTemplate:  
  Type: AWS::EC2::LaunchTemplate  
  Properties:  
    ...  
    KeyName: !Ref KeyPairName
```

This meant I could now SSH directly into any of the spot instances to see how they were doing. I wrote a simple Node.js script to access all of my running instances and check the CPU rate and the hash rate.

Running a command on a remote system and getting the result with NodeJS can be done like this:

So to get the CPU utilisation…

Or the hashrate (as reported in the ethminer.log file)…

I know, these are fragile bits of script and I’ve taken out the catch blocks, but you get the idea.

Using the AWS SDK we can get a list of all the spot instances that are running…

… and when one of these instances doesn’t cut it anymore, we can terminate it:

So using these parts I wrote some code that could run every 20 seconds to grab the CPU/hashrate for all of the spot instances and terminate them if they had a low hashrate or a low CPU usage level for 3 checks in a row. The AutoScalingGroup would then automatically create new spot instances to replace our dead ones. Things were improved.

By now I had been running spot instances for just over 24 hours on my second round of generating Ethereum.

My current unpaid balance: 0.01012 Ether, which means **0.00535 Ether** has been earned in the last **24 hours**.

```
Cost for spot instances = 24 hours * $0.1578 * 5 instances = $18.94
```

*EBS gp2 volumes are 0.10 per GB per month, and we have 100GB per instance. That’s 0.000137 per GB per hour.*  
Cost for EBS volumes = `100 * 0.000137 * 24 * 5 = $1.64`

```
Total cost = $20.58  
Value of Ether mined = $22.10
```

Well that’s good.

Up until now, I hadn’t taken into consideration tax. In the UK, we pay a tax (VAT) of 20% on AWS services (unless we are a company selling our own services and can deduct it) so my actual costs were **$24.70**. Not so good.

But then the next day (12th May 2021) after another 24 hours of running 5 instances I had earned **0.0079 Ether** which had a value of **$33.96** at a cost to me of **$24.70** (including VAT). OK, this is better, but why such a massive difference?

For now, I didn’t question it too much. I applied to AWS to raise my Spot Instance quota/limits in the cheap regions (Ohio, N. Virginia, and Oregon) and checked if there was anything else I could tweak.

I could see that we were paying for 100GB of gp2 storage for each one of these spot instances. They were all using the “Deep Learning AMI (Ubuntu 18.04) Version 36.0” that comes with all the necessary NVIDIA drivers preconfigured. For starters, if I removed the Anaconda Python platform (`~/anaconda3`) from the image then the necessary disk size is reduced to ~36GB so we could get away with a 40GB drive (saving 60% of that EBS storage cost). Also, the newer gp3 storage ($0.08 per GB) is cheaper than gp2 storage ($0.10 per GB). You have to pay extra for gp3 based on how much you use it, but overall it was cheaper for our purpose.

On the 14th of May, by the time I had reached **0.1 Ether** (the minimum at the time to get a payout from Ethermine — the Ethereum mining pool we were using) I was running 40–60 spot instances, dependent on their availability. I had spent just under **$320.70** (including tax) over the last few days to receive 0.1 Ether (**$387.73**).

Press enter or click to view image in full size

![]()

It was at this point I learned about mining profitability:

Press enter or click to view image in full size

![]()

Things were starting to look less exciting:

![]()

Basically, things were changing. Not only did Elon Musk [reply to a tweet with the word “Indeed”](https://twitter.com/elonmusk/status/1394001894809427971) to drop the price of Ethereum back down again, but the dollar-to-hashrate was beginning to normalize again. At the peak of it, I was mining at a cost of **~$183** for 24 hours at 1 GH/s and profitability was at **$282** per day. Since May, profitability has only reached **$111** per GH/s/day (as of 23rd Oct 2021) making this all unprofitable. I pulled the plug at the right time.

The profitability would have to be greater than **$183** per GH/s/day. The profitability is based how many transactions are placed on the network at any given time, and how many miners out there are mining and thereby running the network. The spike in May was put down to a [maelstrom of Elon, DeFi and NFTs](https://www.fool.ca/2021/05/31/ethereum-miner-revenue-hits-new-record-in-may-despite-coin-volatility/) giving miners a lot of work to do. We can calculate the profitability by looking at the time it is taking each block to be mined, and the current hashrate for all the miners on the network, and the current block reward. We can then plug our own hashrate into that and see what size share we are eligible for…

We can get these values from <https://www.etherchain.org/index/data> as well as the current price per Ether in USD.

From that we can calculate the dollar value of mining at 1GH/s/day…

Today (23rd October 2021) the `userDollarPerDay` = **$73.44**. Much less than our **$183** cost.

Even though my 0.1 Ether was worth more than what I’d paid for it at the time, the price of Ether is also clearly very volatile for the foreseeable future. So even if you do mine it whilst it is “profitable” you are gambling that the Ether you are accumulating is going to stay valuable, or at least until you sell it. I managed to sell my Ether at the right price, but not long after it would have been worth much less than I paid for it. All the while burning energy for hours, keeping this big maths game in the sky running, just to break even or throw money to Bezos. It is really not a game worth playing.

YMMV.