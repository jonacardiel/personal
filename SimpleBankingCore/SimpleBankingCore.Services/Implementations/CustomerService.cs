#nullable enable
using System;
using SimpleBankingCore.Core.Models;
using SimpleBankingCore.Data.Repositories;
using SimpleBankingCore.Services.Interfaces;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

namespace SimpleBankingCore.Services.Implementations
{
    public class CustomerService : ICustomerService
    {
        private readonly CustomerRepository _customerRepository;

        public CustomerService(CustomerRepository customerRepository)
        {
            _customerRepository = customerRepository;
        }

        public async Task<Customer> CreateCustomerAsync(string firstName, string lastName, string email)
        {
            var existingCustomer = await _customerRepository.GetByEmailAsync(email);
            if (existingCustomer != null)
            {
                throw new InvalidOperationException($"Customer with email '{email}' already exists.");
            }

            var customer = new Customer
            {
                FirstName = firstName,
                LastName = lastName,
                Email = email
            };
            await _customerRepository.AddAsync(customer);
            await _customerRepository.SaveChangesAsync();
            return customer;
        }

        public async Task<Customer?> GetCustomerByIdAsync(int customerId)
        {
            return await _customerRepository.GetByIdWithAccountsAsync(customerId);
        }

        public async Task<Customer?> GetCustomerByEmailAsync(string email)
        {
            return await _customerRepository.GetByEmailWithAccountsAsync(email);
        }

        public async Task<IEnumerable<Customer>> GetAllCustomersAsync()
        {
            return await _customerRepository.GetAllAsync();
        }
    }
}
 
