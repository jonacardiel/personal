using SimpleBankingCore.Core.Enums;
using System;
using System.Collections.Generic;

namespace SimpleBankingCore.Core.Models
{
    // Represents a bank account
    public class Account
    {
        public int AccountId { get; set; } // Primary Key
        public int CustomerId { get; set; } // Foreign Key to Customer
        public AccountType AccountType { get; set; }
        public decimal CurrentBalance { get; set; } = 0.00m;
        public DateTime DateOpened { get; set; } = DateTime.UtcNow;
        public bool IsActive { get; set; } = true;

        // Navigation properties
        public Customer? Customer { get; set; }
        public ICollection<Transaction> Transactions { get; set; } = new List<Transaction>();
    }
}
