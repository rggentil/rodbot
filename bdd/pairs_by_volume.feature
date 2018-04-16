# Created by rggen at 3/27/2018
Feature: Pairs by volume in 24h
  Rodrigo wants to know the volume (in descending order) of all Cobinhood's pairs.
  Rodrigo, as a user of Cobinhood exchange, wants to know what the volume is for each of the pairs traded in Cobinhood,
  in order to decide which pairs he should trade.

  Background:
    Given there is access to api exchange
    Given rodbot is running

  Scenario: Getting pairs volume 24h
    Then Rodrigo can know the current "BTC-USDT" volume
    Then Rodrigo can know the current "ETH-BTC" volume
    Then Rodrigo can know the current "LTC-BTC" volume

  Scenario: Getting list of pairs by volume in 24h in descending order
    Then Rodrigo can know the list of volumes in descending order

  Scenario: Getting list of pairs with no volume in 24h
    Then Rodrigo can know what pairs don't have volume